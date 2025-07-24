import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using diskpri.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:diskpri.obj=3f5b0bcb39e2b3f5a6044347b46db88aed11508feafce275a68eb7d468eec8e7
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_font_pri_diskpri
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_fontdes_font_pri_diskpri
        +guid:fce37f5b-c8d7-4354-93eb-57b5b03a43ed
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_font_pri_diskpri(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3f5b0bcb39e2b3f5a6044347b46db88aed11508feafce275a68eb7d468eec8e7', timeout=600)
    outputsaver.save_output()
