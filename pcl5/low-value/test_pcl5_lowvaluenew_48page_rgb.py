import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 48Page_rgb.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:48Page-rgb.obj=0c1b2d6554edf75fd2eb788a00fc4b0dae03a8679cc0e5ba2c72892e7fb81b46
    +test_classification:System
    +name: test_pcl5_lowvaluenew_48page_rgb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_lowvaluenew_48page_rgb
        +guid:61f87a40-39e8-4e2a-9805-8a2fecd21752
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

def test_pcl5_lowvaluenew_48page_rgb(setup_teardown, printjob,udw,outputsaver):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('0c1b2d6554edf75fd2eb788a00fc4b0dae03a8679cc0e5ba2c72892e7fb81b46', timeout=600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
