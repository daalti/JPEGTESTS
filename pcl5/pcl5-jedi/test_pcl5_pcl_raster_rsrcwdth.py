import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using rsrcwdth.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rsrcwdth.obj=091b9368764b67fac2cee7ec5124e272a96f84cf4990110854208737d599407e
    +test_classification:System
    +name: test_pcl5_pcl_raster_rsrcwdth
    +test:
        +title: test_pcl5_pcl_raster_rsrcwdth
        +guid:5e7f69f2-4586-4a21-87ed-609514f10140
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_raster_rsrcwdth(setup_teardown, printjob, outputsaver):
    printjob.print_verify('091b9368764b67fac2cee7ec5124e272a96f84cf4990110854208737d599407e', timeout=600)
    outputsaver.save_output()
