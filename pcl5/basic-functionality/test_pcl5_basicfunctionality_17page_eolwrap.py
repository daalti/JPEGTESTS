import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 17Page_eolwrap.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:17Page-eolwrap.obj=4b31947981324884e3aa4a2b6fbdfd6100208b1e18c3af5095078fb69e23807f
    +test_classification:System
    +name: test_pcl5_basicfunctionality_17page_eolwrap
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_17page_eolwrap
        +guid:b4d2e6a9-3927-4f45-8e87-aa858c71b32a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_17page_eolwrap(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4b31947981324884e3aa4a2b6fbdfd6100208b1e18c3af5095078fb69e23807f')
    outputsaver.save_output()
