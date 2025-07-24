import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 22Page_cursmov2.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:22Page-cursmov2.obj=af0ee882d474138ce368892876b249516124142e7588dd76edf78455ea2a3c2a
    +test_classification:System
    +name: test_pcl5_basicfunctionality_22page_cursmov2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_22page_cursmov2
        +guid:dfdf9394-0fef-4389-a3f0-f2b090f6ae82
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_22page_cursmov2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('af0ee882d474138ce368892876b249516124142e7588dd76edf78455ea2a3c2a', timeout=300)
    outputsaver.save_output()
