.pragma library
.import spiceGuiCore 1.0 as SpiceGuiCore

function sidesText(val)
{
    if (val == SpiceGuiCore.Glossary_1_PlexMode.PlexMode.simplex)
    {
        return "1";
    }
    else if (val == SpiceGuiCore.Glossary_1_PlexMode.PlexMode.duplex)
    {
        return "2";
    }
    else
    {
        return "---";
    }
}

function colorText(val)
{
    if (val == SpiceGuiCore.JobTicket_1_ColorModes.ColorModes.color)
    {
        return "Color";
    }
    else if (val == SpiceGuiCore.JobTicket_1_ColorModes.ColorModes.grayscale)
    {
        return "Grayscale";
    }
    else if (val == SpiceGuiCore.JobTicket_1_ColorModes.ColorModes.autoDetect)
    {
        return "Auto detect";
    }
    else if (val == SpiceGuiCore.JobTicket_1_ColorModes.ColorModes.monochrome)
    {
        return "Monochrome";
    }
    else
    {
        return "---";
    }
}

function trayText(val)
{
    if (val == SpiceGuiCore.Glossary_1_MediaSourceId.MediaSourceId.tray_1)
    {
        return "Tray 1";
    }
    else if (val == SpiceGuiCore.Glossary_1_MediaSourceId.MediaSourceId.tray_2)
    {
        return "Tray 2";
    }
    else if (val == SpiceGuiCore.Glossary_1_MediaSourceId.MediaSourceId.tray_3)
    {
        return "Tray 3";
    }
    else if (val == SpiceGuiCore.Glossary_1_MediaSourceId.MediaSourceId.autoselect)
    {
        return "Automatic";
    }
    else
    {
        return "---";
    }
}

function sizeText(val)
{
    if (val == SpiceGuiCore.Glossary_1_MediaSize.MediaSize.iso_a5_148x210mm)
    {
        return "A5";
    }
    else if (val == SpiceGuiCore.Glossary_1_MediaSize.MediaSize.iso_a4_210x297mm)
    {
        return "A4";
    }
    else if (val == SpiceGuiCore.Glossary_1_MediaSize.MediaSize.na_letter_8_5x11in)
    {
        return "Letter";
    }
    else if (val == SpiceGuiCore.Glossary_1_MediaSize.MediaSize.na_legal_8_5x14in)
    {
        return "Legal";
    }
    else
    {
        return "---";
    }
}

function collateText(val)
{
    if (val == SpiceGuiCore.JobTicket_1_CollateModes.CollateModes.collated)
    {
        return "Collated";
    }
    else if (val == SpiceGuiCore.JobTicket_1_CollateModes.CollateModes.uncollated)
    {
        return "Uncollated";
    }
    else
    {
        return "---";
    }
}

function mediaTypeText(val)
{
    if (val == SpiceGuiCore.Glossary_1_MediaType.MediaType.custom)
    {
        return "Custom";
    }
    else if (val == SpiceGuiCore.Glossary_1_MediaType.MediaType.stationery)
    {
        return "Plain";
    }
    else
    {
        return "---";
    }
}
