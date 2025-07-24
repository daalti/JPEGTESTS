import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using fontlist.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fontlist.pcl=89f14da0945f81b02f3fe6f529727274921bcfb103df2ba05cc546796bc5ce7c
    +test_classification:System
    +name: test_pcl5_allocidcoverage_fontlist
    +test:
        +title: test_pcl5_allocidcoverage_fontlist
        +guid:a2268265-b110-4a3f-a1ae-006c1413d59a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_fontlist(setup_teardown, printjob, outputsaver):
    printjob.print_verify('89f14da0945f81b02f3fe6f529727274921bcfb103df2ba05cc546796bc5ce7c', timeout=600)
    outputsaver.save_output()
