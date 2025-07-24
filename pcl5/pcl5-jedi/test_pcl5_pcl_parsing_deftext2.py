import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using deftext2.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:deftext2.obj=baa5eff063761f3eeb9f08bbf94ee8f1726c2d79c8e97f324e40b8feeb0cfc7d
    +test_classification:System
    +name: test_pcl5_pcl_parsing_deftext2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_parsing_deftext2
        +guid:6ddf926d-5fc9-423d-9682-19c74a49755d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_parsing_deftext2(udw, setup_teardown, printjob, outputsaver):
    # printjob.print_verify('baa5eff063761f3eeb9f08bbf94ee8f1726c2d79c8e97f324e40b8feeb0cfc7d', timeout=900)
    # outputsaver.save_output()
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify_multi('baa5eff063761f3eeb9f08bbf94ee8f1726c2d79c8e97f324e40b8feeb0cfc7d', timeout=600,expected_jobs=7)
    else:
        printjob.print_verify('baa5eff063761f3eeb9f08bbf94ee8f1726c2d79c8e97f324e40b8feeb0cfc7d', timeout=600)
    outputsaver.save_output()
