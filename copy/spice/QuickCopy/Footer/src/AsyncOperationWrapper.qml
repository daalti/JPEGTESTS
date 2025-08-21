
import QtQuick 2.15

QtObject {
    id: asyncOperationWrapper
    property var _futureX: null
    property var asyncOperation: null 
    signal resolved(var future)
    signal rejected(var future)

    function resolve(future) {
        if(asyncOperationWrapper) resolved(future)
    }

    function reject(future) {
        if(asyncOperationWrapper) rejected(future)
    }

    Component.onCompleted: {
        if (typeof asyncOperation === "function") {
            _futureX = asyncOperation()
            if (_futureX && _futureX.resolved && _futureX.rejected) {
                _futureX.resolved.connect(asyncOperationWrapper.resolve)
                _futureX.rejected.connect(asyncOperationWrapper.reject)
            }
            else {
                console.error("Invalid future object returned by asyncOperation")
            }
        }
        else {
            console.error("asyncOperation is not a function")
        }
    }

    Component.onDestruction: {
        if(_futureX)
        {
            _futureX.resolved.disconnect(resolve)
            _futureX.rejected.disconnect(reject)
        }
    }
}