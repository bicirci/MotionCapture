
function ContentFragmentContainerCustomCallback(variableName, callbackFunction, authHeaderCookieName) {
    this._variableName = variableName;
    this._callbackFunction = callbackFunction;
    this._authHeaderCookieName = authHeaderCookieName;
}

ContentFragmentContainerCustomCallback.prototype._getAuthValue = function () {
    var nameEQ = this._authHeaderCookieName + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return '';
}

ContentFragmentContainerCustomCallback.prototype._customCallback = function (id, callbackControlId, callbackParameter, callbackContext, successFunction, errorFunction) {
    this._callbackFunction('custom', 'id=' + encodeURIComponent(id) + '&renderFromCurrent=True&callback_control_id=' + encodeURIComponent(callbackControlId) + '&callback_argument=' + encodeURIComponent(callbackParameter), successFunction, errorFunction, callbackContext, this._getAuthValue());
}
