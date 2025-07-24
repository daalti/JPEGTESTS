import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_Chrome_AutoMD_Lighter_text_UPD_5_7_0_PCL5.prn
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-Chrome_-_AutoMD_-_Lighter_text_-_UPD_5.7.0_PCL5.prn=f786a751068663b9eefe087946eb8c093ebdc4ec5d78fdedc380de7163a3589c
    +test_classification:System
    +name: test_pcl5_highvalue_1page_chrome_automd_lighter_text_upd_5_7_0_pcl5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_chrome_automd_lighter_text_upd_5_7_0_pcl5
        +guid:ad1b46cc-4abe-4a2d-b171-ec63bdda71cc
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

def test_pcl5_highvalue_1page_chrome_automd_lighter_text_upd_5_7_0_pcl5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f786a751068663b9eefe087946eb8c093ebdc4ec5d78fdedc380de7163a3589c')
    outputsaver.save_output()
