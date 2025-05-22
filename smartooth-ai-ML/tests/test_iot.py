import pytest
from app.iot_integration import ToothbrushTracker

@pytest.fixture
def tracker():
    return ToothbrushTracker()

def test_iot_data_processing(tracker):
    test_data = [
        {'duration': 120, 'pressure': 50, 'coverage': 80},
        {'duration': 150, 'pressure': 55, 'coverage': 85}
    ]
    result = tracker.process_brushing_data('test_device', test_data)
    assert result['metrics']['daily_brushing_sessions'] == 2
    assert 60 <= result['metrics']['avg_duration'] <= 80