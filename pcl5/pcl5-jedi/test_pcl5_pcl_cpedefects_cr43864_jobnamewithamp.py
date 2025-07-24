import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using JobNameWithAmp.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:JobNameWithAmp.pcl=625b148f1c8a268d5eaf3deca3a0231c72a43706ac51509ef47cc07f6ccf2c7a
    +test_classification:System
    +name: test_pcl5_pcl_cpedefects_cr43864_jobnamewithamp
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_cpedefects_cr43864_jobnamewithamp
        +guid:fc7ce99f-15ec-4e41-8594-f85c9321579c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_cpedefects_cr43864_jobnamewithamp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('625b148f1c8a268d5eaf3deca3a0231c72a43706ac51509ef47cc07f6ccf2c7a', timeout=600)
    outputsaver.save_output()
