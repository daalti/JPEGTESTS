import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 0Page_fontchk.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:0Page-fontchk.obj=2e8d710ff6a103ff8bfcb442470d2fc8eed39cb9f9cc7413be6a43a227cc92ce
    +test_classification:System
    +name: test_pcl5_highvalue_0page_fontchk
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_0page_fontchk
        +guid:0fde3eb6-68f8-4358-b888-6f7a2ae09620
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


    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_0page_fontchk(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2e8d710ff6a103ff8bfcb442470d2fc8eed39cb9f9cc7413be6a43a227cc92ce', timeout=1500)
    outputsaver.save_output()
