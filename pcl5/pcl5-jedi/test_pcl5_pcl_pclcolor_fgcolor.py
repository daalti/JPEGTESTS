import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fgcolor.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:fgcolor.obj=59c0fe5bfe850e8917eff2caa9a4eb5489cd6358c6b772fc89373fa91ce58c72
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_fgcolor
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_pclcolor_fgcolor
        +guid:ffd4d1a2-4e1c-429d-871a-ca0723944115
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_fgcolor(setup_teardown, printjob, outputsaver):
    printjob.print_verify('59c0fe5bfe850e8917eff2caa9a4eb5489cd6358c6b772fc89373fa91ce58c72', timeout=600)
    outputsaver.save_output()
