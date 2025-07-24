import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using textpars83.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:textpars83.obj=93a2de92383a37f75017360082e6d49a897318a9cfd7cced2ca6968f368c6801
    +test_classification:System
    +name: test_pcl5_pcl_parsing_textpars83
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_parsing_textpars83
        +guid:b16866ea-868b-4ed4-9f1a-be47ca3f0194
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_parsing_textpars83(udw, setup_teardown, printjob, outputsaver):
    # printjob.print_verify('93a2de92383a37f75017360082e6d49a897318a9cfd7cced2ca6968f368c6801', timeout=700)
    # outputsaver.save_output()
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify_multi('93a2de92383a37f75017360082e6d49a897318a9cfd7cced2ca6968f368c6801', timeout=600,expected_jobs=5)
    else:
        printjob.print_verify('93a2de92383a37f75017360082e6d49a897318a9cfd7cced2ca6968f368c6801', timeout=600)
    outputsaver.save_output()
