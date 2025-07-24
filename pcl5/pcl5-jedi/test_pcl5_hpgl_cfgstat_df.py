import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using df.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:df.obj=2f3d67438dd745c5289cc0bb7666fef5d43b9ffe660a899c00e0d7a841aa3fab
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_df
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_hpgl_cfgstat_df
        +guid:1462c4e1-9775-494c-9282-cc1439506500
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_df(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2f3d67438dd745c5289cc0bb7666fef5d43b9ffe660a899c00e0d7a841aa3fab', timeout=600)
    outputsaver.save_output()
