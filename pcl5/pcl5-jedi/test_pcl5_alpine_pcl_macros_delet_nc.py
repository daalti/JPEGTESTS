import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 alpine using delet_nc.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:delet_nc.obj=68e35ae2f5b9e3d9612ee90221bdfd94477e8ea9ca58daf919887649ab29ab1f
    +test_classification:System
    +name: test_pcl5_alpine_pcl_macros_delet_nc
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_alpine_pcl_macros_delet_nc
        +guid:c00a9633-03be-4325-bd7d-1f544aae5b33
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_alpine_pcl_macros_delet_nc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('68e35ae2f5b9e3d9612ee90221bdfd94477e8ea9ca58daf919887649ab29ab1f', timeout=600)
    outputsaver.save_output()
