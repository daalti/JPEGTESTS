import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using jppmin.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jppmin.obj=a3798d00ac083710c56a45e81e0ee6ec32b695ff912e3c59638c99952e2680f0
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_jppmin
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_jppmin
        +guid:2b4ef169-7867-4346-ab22-2dc986c3f4fc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_jppmin(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a3798d00ac083710c56a45e81e0ee6ec32b695ff912e3c59638c99952e2680f0', timeout=600)
    outputsaver.save_output()
