import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:R600_pcl_Hagaki_Postcard_Simplex_34494-hagaki_PCL5-5.0.3.prn=86caa399c49d18f7711d719d69a045a1e0eabed957e7d9a1ee60c11ddb9189cd
    +name:test_pcl5_r600_pcl_hagaki_postcard_simplex_34494_hagaki_pcl5_5_0_3_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_r600_pcl_hagaki_postcard_simplex_34494_hagaki_pcl5_5_0_3_prn
        +guid:64798b8e-b731-470c-8e01-621e4f4c31aa
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_r600_pcl_hagaki_postcard_simplex_34494_hagaki_pcl5_5_0_3_prn(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('jpn_hagaki_100x148mm','tray-1'):
        tray.configure_tray('tray-1', 'jpn_hagaki_100x148mm', 'any')
    printjob.print_verify_multi('86caa399c49d18f7711d719d69a045a1e0eabed957e7d9a1ee60c11ddb9189cd')
    outputsaver.save_output()