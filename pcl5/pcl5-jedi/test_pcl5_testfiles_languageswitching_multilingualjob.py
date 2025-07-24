import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using multilingualjob.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:multilingualjob.pcl=2f8eac288db125a657a03823cf989234c086f2569eaf424b23f6f20c4083997d
    +test_classification:System
    +name: test_pcl5_testfiles_languageswitching_multilingualjob
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_languageswitching_multilingualjob
        +guid:b57b9658-2941-48f3-8a62-19cc66e95b36
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_languageswitching_multilingualjob(udw, setup_teardown, printjob, outputsaver):
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify_multi('2f8eac288db125a657a03823cf989234c086f2569eaf424b23f6f20c4083997d', timeout=600,expected_jobs=3)
    else:
        printjob.print_verify('2f8eac288db125a657a03823cf989234c086f2569eaf424b23f6f20c4083997d', timeout=600)
    outputsaver.save_output()
