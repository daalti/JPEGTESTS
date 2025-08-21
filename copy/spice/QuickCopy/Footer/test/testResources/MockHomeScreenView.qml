import QtQuick 2.15
import spiceux 1.0

Rectangle{
    id: mockHomeScreenView
    width: 200
    height: 200
    property Component homeScreenFooterRightComponent: null

    function emitHomescreenViewReady()
    {
        Global.homeScreenViewReady()
    }
}