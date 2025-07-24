import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using rastcomp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rastcomp.obj=6ba44362c1e6e593637a799c39f70016a9ac53eec83f556d2000a77fc331a2fe
    +test_classification:System
    +name: test_pcl5_pcl_raster_rastcomp
    +test:
        +title: test_pcl5_pcl_raster_rastcomp
        +guid:04c3b07a-c974-4cec-bd96-e21cb1c8610b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_raster_rastcomp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6ba44362c1e6e593637a799c39f70016a9ac53eec83f556d2000a77fc331a2fe', timeout=900)
    outputsaver.save_output()
