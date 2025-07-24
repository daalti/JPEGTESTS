import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using Intfonts.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:Intfonts.pcl=0ca5bd8577e83a1148f10deee13448bf66cd7126ffa4234beebb7c364484dbd0
    +test_classification:System
    +name: test_pcl5_testfiles_text_intfonts
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_text_intfonts
        +guid:bb7f53da-c297-4426-9d6f-86c85e292acd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_text_intfonts(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0ca5bd8577e83a1148f10deee13448bf66cd7126ffa4234beebb7c364484dbd0', timeout=600)
    outputsaver.save_output()
