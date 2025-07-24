import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sb.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sb.obj=74595842fbad2577fc7bbe153040128bb9e2edc57e781b2b11e12ccafe259a46
    +test_classification:System
    +name: test_pcl5_hpgl_char_sb
    +test:
        +title: test_pcl5_hpgl_char_sb
        +guid:1a12685f-dbbf-47c6-9582-3a1e8d21d087
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_sb(setup_teardown, printjob, outputsaver):
    printjob.print_verify('74595842fbad2577fc7bbe153040128bb9e2edc57e781b2b11e12ccafe259a46', timeout=600)
    outputsaver.save_output()
