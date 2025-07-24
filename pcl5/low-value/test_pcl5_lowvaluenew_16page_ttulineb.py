import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 16Page_ttulineb.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:16Page-ttulineb.obj=449f26e9217efb5a25d8052b308d8d14d910ff4b104251b04ce1ecff539bd97e
    +test_classification:System
    +name: test_pcl5_lowvaluenew_16page_ttulineb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_lowvaluenew_16page_ttulineb
        +guid:d9e72b62-d45f-45d8-a0a3-20e6c964c1f9
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

def test_pcl5_lowvaluenew_16page_ttulineb(setup_teardown, printjob, outputsaver,udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('449f26e9217efb5a25d8052b308d8d14d910ff4b104251b04ce1ecff539bd97e', timeout=600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
