import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 16Page_in.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:16Page-in.obj=36f6ce0b9a67c54b33e87379ee05446821eb45fb45409a44d86deb68ba3b180c
    +test_classification:System
    +name: test_pcl5_basicfunctionality_16page_in
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_16page_in
        +guid:5a9b2436-e676-49a5-85ca-c0d907e64cee
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

def test_pcl5_basicfunctionality_16page_in(setup_teardown, printjob, outputsaver,udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('36f6ce0b9a67c54b33e87379ee05446821eb45fb45409a44d86deb68ba3b180c', timeout=300)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
