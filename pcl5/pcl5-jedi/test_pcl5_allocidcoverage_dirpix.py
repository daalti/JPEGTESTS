import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using dirpix.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dirpix.pcl=8e42efbae87c2176a0708a980f26b466a9bd17be9683112c1b1b0bbd6bcae832
    +test_classification:System
    +name: test_pcl5_allocidcoverage_dirpix
    +test:
        +title: test_pcl5_allocidcoverage_dirpix
        +guid:a7b735cc-9260-4052-a3c1-45372697e4d4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_dirpix(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8e42efbae87c2176a0708a980f26b466a9bd17be9683112c1b1b0bbd6bcae832', timeout=600)
    outputsaver.save_output()
