import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 17Page_ftbyt18.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:17Page-ftbyt18.obj=b36c51a74417b7169528c9b0ad5208b157c911fafdddaaa5c038b250d3e878d3
    +test_classification:System
    +name: test_pcl5_highvalue_17page_ftbyt18
    +test:
        +title: test_pcl5_highvalue_17page_ftbyt18
        +guid:83f57600-e85e-485d-b503-bb944571870f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_17page_ftbyt18(setup_teardown, printjob, counters, outputsaver):
    printjob.print_verify_multi('b36c51a74417b7169528c9b0ad5208b157c911fafdddaaa5c038b250d3e878d3',timeout=600)
    outputsaver.save_output()
