import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using rasbars2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:800
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rasbars2.obj=6ed586c504a07e68953019c6108b6bc7ba271dacae27f747d69fbfb9eb9de718
    +test_classification:System
    +name: test_pcl5_pcl_raster_rasbars_rasbars2
    +test:
        +title: test_pcl5_pcl_raster_rasbars_rasbars2
        +guid:ea580a81-4d42-4c6a-ae3e-6e9fd40220d6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_raster_rasbars_rasbars2(udw, setup_teardown, printjob, outputsaver):
    # printjob.print_verify('6ed586c504a07e68953019c6108b6bc7ba271dacae27f747d69fbfb9eb9de718', timeout=600)
    # outputsaver.save_output()
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify_multi('6ed586c504a07e68953019c6108b6bc7ba271dacae27f747d69fbfb9eb9de718', timeout=800,expected_jobs=11)
    else:
        printjob.print_verify('6ed586c504a07e68953019c6108b6bc7ba271dacae27f747d69fbfb9eb9de718', timeout=600)
    outputsaver.save_output()
