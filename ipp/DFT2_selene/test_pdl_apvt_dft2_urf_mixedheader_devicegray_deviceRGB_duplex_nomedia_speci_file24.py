import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile24.urf=2c7ac9e5c89c9ec90986f90942a482aea84b546f14f78f58ba6bfc503cee3221
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_mixedheader_devicegray_deviceRGB_duplex_nomedia_speci_file24
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_mixedheader_devicegray_deviceRGB_duplex_nomedia_speci_file24
        +guid:b64ed3b2-e598-49fe-881e-c828ffc40aa9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_mixedheader_devicegray_deviceRGB_duplex_nomedia_speci_file24(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_mixedheader_devicegray_deviceRGB_duplex_nomedia_speci_file24.test', '2c7ac9e5c89c9ec90986f90942a482aea84b546f14f78f58ba6bfc503cee3221')
    outputsaver.save_output()