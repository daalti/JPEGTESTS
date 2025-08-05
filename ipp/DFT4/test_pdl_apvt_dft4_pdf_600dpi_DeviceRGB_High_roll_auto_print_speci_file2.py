import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile2.pdf=212bb156df70fbfdcc5d5d98611aaad74267110711d7952cfbb954cff838150f
    +test_classification:System
    +name:test_pdl_apvt_dft4_pdf_600dpi_DeviceRGB_High_roll_auto_print_speci_file2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft4_pdf_600dpi_DeviceRGB_High_roll_auto_print_speci_file2
        +guid:52075644-ffc2-4191-b2d8-208c3d98f903
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & MediaInputInstalled=MainRoll & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft4_pdf_600dpi_DeviceRGB_High_roll_auto_print_speci_file2(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft4_pdf_600dpi_DeviceRGB_High_roll_auto_print_speci_file2.test', '212bb156df70fbfdcc5d5d98611aaad74267110711d7952cfbb954cff838150f')
    outputsaver.save_output()