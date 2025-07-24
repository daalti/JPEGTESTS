import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 8Page_gl.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:8Page-gl.obj=c61e9d843177429bea0da78aa5b48154203ceb6e8eaffd935dd93115d90096a6
    +test_classification:System
    +name: test_pcl5_lowvaluenew_8page_gl
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_lowvaluenew_8page_gl
        +guid:6bf6517d-c451-4c1f-916d-63456d1ad69e
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

def test_pcl5_lowvaluenew_8page_gl(setup_teardown, printjob,udw,outputsaver):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('c61e9d843177429bea0da78aa5b48154203ceb6e8eaffd935dd93115d90096a6', timeout=600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    
