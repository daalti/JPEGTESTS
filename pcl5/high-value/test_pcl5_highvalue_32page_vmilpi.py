import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 32Page_vmilpi.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:32Page-vmilpi.obj=15c77ca9858c78919d8edff43b8217208ac398a90726315fbf34e196234e2d7f
    +test_classification:System
    +name: test_pcl5_highvalue_32page_vmilpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_32page_vmilpi
        +guid:bb730bcc-e06f-49d6-acc9-4c12ad2b0a0e
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

def test_pcl5_highvalue_32page_vmilpi(setup_teardown, printjob, outputsaver):
    printjob.print_verify('15c77ca9858c78919d8edff43b8217208ac398a90726315fbf34e196234e2d7f', timeout=600)
    outputsaver.save_output()
