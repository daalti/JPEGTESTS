import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygungf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygungf.obj=cbe3fcd8bfa5b5cb103a7aa2847bc1850a843e37fe3896d59f770fd18a652219
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygungf
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygungf
        +guid:42c07759-d678-4d39-a738-0a5ca7f9d882
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygungf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cbe3fcd8bfa5b5cb103a7aa2847bc1850a843e37fe3896d59f770fd18a652219', timeout=600)
    outputsaver.save_output()
