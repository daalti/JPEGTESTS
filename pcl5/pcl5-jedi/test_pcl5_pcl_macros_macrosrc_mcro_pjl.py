import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using mcro_pjl.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:mcro_pjl.obj=4c03cb2e8a545cdd24323aac865d333d04b6376af5538b2939725e831fa86dab
    +test_classification:System
    +name: test_pcl5_pcl_macros_macrosrc_mcro_pjl
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_macros_macrosrc_mcro_pjl
        +guid:364c21fb-758a-4c16-8594-2e872219fcb9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_macros_macrosrc_mcro_pjl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4c03cb2e8a545cdd24323aac865d333d04b6376af5538b2939725e831fa86dab', timeout=600)
    outputsaver.save_output()
