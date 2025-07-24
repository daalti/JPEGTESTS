import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 231Page_genoafts.obj
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:231Page-genoafts.obj=291962c8c92c06dc3b056b6cc3d500d0b826234103d60c4e8c50f0d3d6b092ec
    +test_classification:System
    +name: test_pcl5_basicfunctionality_231page_genoafts
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_231page_genoafts
        +guid:7b8ffc72-4c46-4fa2-b450-e49ad788ecdb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_231page_genoafts(setup_teardown, printjob, outputsaver):
    printjob.print_verify('291962c8c92c06dc3b056b6cc3d500d0b826234103d60c4e8c50f0d3d6b092ec',timeout=3200)
    outputsaver.save_output()
