import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_IE___VZW___Success___UPD_5_7_0_PCL5.prn
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-IE_-_VZW_-_Success_-_UPD_5.7.0_PCL5.prn=2652a046cd23542a8e92bf5b8bab28761e188a5743184d95280c77492e145489
    +test_classification:System
    +name: test_pcl5_highvalue_1page_ie_vzw_success_upd_5_7_0_pcl5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_ie_vzw_success_upd_5_7_0_pcl5
        +guid:83ba2b3c-52a1-490d-b404-7df78fe122ab
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

def test_pcl5_highvalue_1page_ie_vzw_success_upd_5_7_0_pcl5(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('2652a046cd23542a8e92bf5b8bab28761e188a5743184d95280c77492e145489', timeout=600)
    outputsaver.save_output()
    current_crc = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(current_crc)
