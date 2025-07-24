import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using rastmode.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rastmode.obj=e34be6754ad32123eb84410f023d93e48bbc1a7b37a45d3fd000cd7de59e71bd
    +test_classification:System
    +name: test_pcl5_pcl_raster_rastmode
    +test:
        +title: test_pcl5_pcl_raster_rastmode
        +guid:2cc3ce0c-0048-4d65-882b-0e7231c2488a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_raster_rastmode(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e34be6754ad32123eb84410f023d93e48bbc1a7b37a45d3fd000cd7de59e71bd', timeout=600)
    outputsaver.save_output()
