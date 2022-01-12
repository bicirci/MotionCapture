package random1.comp6733;

import android.content.Context;
import android.content.res.Resources;

public class SensorItemData {
    // data storage to map to its equivalent UI element
    private String mSensorTitle;
    private String mSensorMacValue;
    private String mSensorUuidValue;
    private boolean mEnableSensor;
    private String mSensorBodyValue;

    SensorItemData(Context context) {
        // set defaults
        Resources res = context.getResources();
        this.mSensorTitle = res.getString(R.string.stringSensorTitle);
        this.mSensorMacValue = res.getString(R.string.stringUnknown);
        this.mSensorUuidValue = res.getString(R.string.stringUnknown);
        this.mEnableSensor = false;
        String[] bodyParts = res.getStringArray(R.array.bodyParts);
        if (bodyParts.length > 0) this.mSensorBodyValue = bodyParts[0];
        // NOTE: you should check that this is consistent with the Adapter
    }

    SensorItemData(String sensorTitle, String mac, String uuid, boolean enabled, String bodyValue) {
        this.mSensorTitle = sensorTitle;
        this.mSensorMacValue = mac;
        this.mSensorUuidValue = uuid;
        this.mEnableSensor = enabled;
        this.mSensorBodyValue = bodyValue;
    }

    // ------------------------------------------------------------------------------------------
    // getters
    public String getTitle() {
        return mSensorTitle;
    }

    public String getMac() {
        return mSensorMacValue;
    }

    public String getUuid() {
        return mSensorUuidValue;
    }

    public boolean isEnabled() {
        return mEnableSensor;
    }

    public String getBodyValue() {
        return mSensorBodyValue;
    }

    // setters
    public void setTitle(String mSensorTitle) {
        this.mSensorTitle = mSensorTitle;
    }

    public void setMac(String mSensorMacValue) {
        this.mSensorMacValue = mSensorMacValue;
    }

    public void setUuid(String mSensorUuidValue) {
        this.mSensorUuidValue = mSensorUuidValue;
    }

    public void setEnabled(boolean mEnableSensor) {
        this.mEnableSensor = mEnableSensor;
    }

    public void setBodyValue(String mSensorBodyValue) {
        this.mSensorBodyValue = mSensorBodyValue;
    }
}
