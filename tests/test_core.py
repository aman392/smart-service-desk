from core import process, validate_request


def test_missing_address_requires_review():
    result = process("Repair AC-204 urgently. Call 9876543210.")
    assert result["status"] == "Needs review"
    assert "Service address required" in result["issues"]


def test_valid_service_request():
    result = process("Repair AC-204 at 12 Market Street, Raipur. Call 9876543210.")
    assert result["extraction"]["category"] == "repair"
    assert result["status"] == "Ready for manual dispatch review"


def test_no_hallucinated_contact():
    record = {"category": "quotation", "priority": "normal", "asset_id": None,
              "address": None, "contact_phone": "9876543210", "summary": "test"}
    result = validate_request(record, "Please send a quote.")
    assert result["status"] == "Needs review"
    assert "Contact number not found in original request" in result["issues"]


def test_empty_input_rejected():
    try:
        process(" ")
        assert False, "should fail"
    except ValueError:
        pass


def test_cancellation_requires_manual_review():
    message = "Please cancel my previous repair request for pump P-17."
    result = process(message)

    assert result["status"] == "Needs review"
    assert result["extraction"]["category"] == "other"
    assert result["extraction"]["asset_id"] == "P-17"
    assert "Cancellation request detected" in result["issues"][0]
    assert "Service address required" not in result["issues"]
    assert "Valid 10-digit contact number required" not in result["issues"]
