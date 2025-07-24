import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using gcusrprog.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:gcusrprog.pcl=2e4dda1b1e423540a266b1e4d00d6b895cdd3d3a34e4f7d15170d7057a805fc6
    +test_classification:System
    +name: test_pcl5_testfiles_gcusrprog
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_gcusrprog
        +guid:aaba9bf4-e9d3-4380-bd22-02a05bb24430
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gcusrprog(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2e4dda1b1e423540a266b1e4d00d6b895cdd3d3a34e4f7d15170d7057a805fc6', timeout=600)
    outputsaver.save_output()
