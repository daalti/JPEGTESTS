import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using lsg55412_jedi.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:lsg55412_jedi.obj=e4de3a73235334f72742ca56e76a4b3538b9093adccda95007eefff88bff2d3d
    +test_classification:System
    +name: test_pcl5_pcl_cpedefects_lsg55412_lsg55412_jedi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_cpedefects_lsg55412_lsg55412_jedi
        +guid:b8cf3cd6-15d9-4fc2-8bda-fa52877ba15f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_cpedefects_lsg55412_lsg55412_jedi(udw, setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('e4de3a73235334f72742ca56e76a4b3538b9093adccda95007eefff88bff2d3d', timeout=600,expected_jobs=4)
    outputsaver.save_output()