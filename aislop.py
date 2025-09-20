import firebase_admin
from firebase_admin import credentials, firestore
import time
import sys
import logging
from google.api_core.exceptions import DeadlineExceeded, Aborted

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Constants / Config
BATCH_SIZE = 500  # Firestore limits: 500 writes per batch
RETRY_DELAY_SEC = 5
MAX_RETRIES = 5
COPY_SUBCOLLECTIONS = True  # if you want to copy nested subcollections

# Initialize source & destination apps
def init_firestore_app(service_account_key_file, app_name=None):
    cred = credentials.Certificate(service_account_key_file)
    # If same default app name, you need to give name param to avoid collision
    return firebase_admin.initialize_app(cred, name=app_name)  # name=None means default

def get_client(app):
    return firestore.client(app)

def copy_collection(src_col_ref, dst_col_ref):
    """
    Copy documents from src_col_ref to dst_col_ref, in batches.
    Returns number of docs copied.
    """
    docs = list(src_col_ref.stream())
    total = len(docs)
    logging.info(f"Found {total} documents in source collection {src_col_ref.id}")

    copied = 0
    batch = None
    writes_in_batch = 0
    for doc in docs:
        if batch is None:
            batch = dst_col_ref._client.batch()

        # Overwrite existing document. Could add check if exist to skip.
        batch.set(dst_col_ref.document(doc.id), doc.to_dict())
        writes_in_batch += 1

        if writes_in_batch == BATCH_SIZE:
            commit_with_retry(batch)
            copied += writes_in_batch
            writes_in_batch = 0
            batch = None
            logging.info(f"Copied {copied}/{total} documents in collection {src_col_ref.id}")

    # commit leftover
    if batch is not None and writes_in_batch > 0:
        commit_with_retry(batch)
        copied += writes_in_batch
        logging.info(f"Copied total {copied}/{total} documents in collection {src_col_ref.id}")

    return copied

def commit_with_retry(batch):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            batch.commit()
            return
        except (DeadlineExceeded, Aborted) as e:
            logging.warning(f"Batch commit attempt {attempt} failed with {e}. Retrying after delay.")
            time.sleep(RETRY_DELAY_SEC)
    # after retries
    logging.error("Failed to commit batch after retries.")
    raise RuntimeError("Batch commit failed")

def copy_subcollections_for_document(src_doc_ref, dst_doc_ref):
    """
    Recursively copy subcollections of a document.
    Note: Firestore does not provide listing subcollections directly in Admin SDK
    except via list_collections() on DocumentReference.
    """
    try:
        for subcol in src_doc_ref.collections():
            dst_subcol_ref = dst_doc_ref.collection(subcol.id)
            logging.info(f"Copying subcollection {subcol.id} under document {src_doc_ref.id}")
            copy_collection(subcol, dst_subcol_ref)

            if COPY_SUBCOLLECTIONS:
                # For each document in this subcollection, recurse further
                for subdoc in subcol.stream():
                    src_subdoc_ref = subcol.document(subdoc.id)
                    dst_subdoc_ref = dst_subcol_ref.document(subdoc.id)
                    copy_subcollections_for_document(src_subdoc_ref, dst_subdoc_ref)
    except Exception as e:
        logging.error(f"Error copying subcollections for document {src_doc_ref.id}: {e}")
        raise

def migrate(
    source_service_key_file: str,
    dest_service_key_file: str,
    collections_to_copy: list = None,
    overwrite: bool = True
):
    """
    Perform migration from source Firestore → destination Firestore.

    :param collections_to_copy: list of collection names (strings). If None, copy all top-level collections.
    :param overwrite: if True, destination documents are overwritten. If False, existing docs are skipped.
    """
    # initialize apps and clients
    src_app = init_firestore_app(source_service_key_file, app_name="source")
    dst_app = init_firestore_app(dest_service_key_file, app_name="destination")

    src_db = get_client(src_app)
    dst_db = get_client(dst_app)

    # determine collections to copy
    if collections_to_copy is None:
        # get all top level collections
        collections_to_copy = [col.id for col in src_db.collections()]
        logging.info(f"No collections_to_copy specified. Will migrate all top-level collections: {collections_to_copy}")
    else:
        logging.info(f"Migrating specified collections: {collections_to_copy}")

    total_docs = 0

    for col_name in collections_to_copy:
        src_col_ref = src_db.collection(col_name)
        dst_col_ref = dst_db.collection(col_name)
        logging.info(f"Starting copy for collection: {col_name}")
        num = copy_collection(src_col_ref, dst_col_ref)
        total_docs += num
        logging.info(f"Finished copy for collection {col_name}, docs copied: {num}")

        if COPY_SUBCOLLECTIONS:
            # copy subcollections
            for doc in src_col_ref.stream():
                src_doc_ref = src_col_ref.document(doc.id)
                dst_doc_ref = dst_col_ref.document(doc.id)
                copy_subcollections_for_document(src_doc_ref, dst_doc_ref)

    logging.info(f"Migration complete. Total documents copied: {total_docs}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate Firestore data from one project to another.")
    parser.add_argument(
        "--source_key",
        required=True,
        help="Path to service account JSON for source Firestore project"
    )
    parser.add_argument(
        "--dest_key",
        required=True,
        help="Path to service account JSON for destination Firestore project"
    )
    parser.add_argument(
        "--collections",
        nargs="*",
        help="Collection names to migrate. If omitted, all top-level collections are migrated."
    )
    parser.add_argument(
        "--no_overwrite",
        action="store_true",
        help="If set, existing documents in destination will not be overwritten."
    )
    args = parser.parse_args()

    migrate(
        source_service_key_file=args.source_key,
        dest_service_key_file=args.dest_key,
        collections_to_copy=args.collections,
        overwrite=not args.no_overwrite
    )
