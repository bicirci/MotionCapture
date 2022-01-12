package random1.comp6733;

import android.app.Activity;
import android.content.Context;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;

import androidx.core.content.res.ResourcesCompat;

// don't care about getter/setter validation
// tracks all useful content in the sensor item view

public class SensorItemComponents {
    private final String TAG = "SensorItemComponents";
    // data components
    public TextView mSensorTitle;       // device name
    public TextView mSensorMacValue;    // device MAC addr
    public TextView mSensorUuidValue;   // device BLE UUID
    public CheckBox mEnableSensor;      // true if device to be used
    public Spinner mSensorBodyValue;    // select body part location
    // visual formatting
    public LinearLayout mSensorItemLayout; // outer frame of 'card'
    public int mColorBackgroundDefault;
    public int mColorBackgroundEnabled;
    // metadata to data
    public SensorItemData mDataRef;
    private ArrayAdapter<CharSequence> mSensorBodyValueArray;

    // ------------------------------------------------------------------------------------------
    public void setComponents(View finder) {
        Context con = finder.getContext();
        this.mSensorTitle = (TextView)finder.findViewById(R.id.sensorTitle);
        this.mSensorMacValue = (TextView)finder.findViewById(R.id.sensorMacValue);
        this.mSensorUuidValue = (TextView)finder.findViewById(R.id.sensorUuidValue);
        this.mEnableSensor = (CheckBox)finder.findViewById(R.id.enableSensor);
        this.mSensorBodyValue = (Spinner)finder.findViewById(R.id.sensorBodyValue);
        // visual formatting
        this.mSensorItemLayout = finder.findViewById(R.id.sensorItemLayout);
        this.mColorBackgroundDefault = ResourcesCompat.getColor(finder.getResources(),
                R.color.colorSensorItemBackground, null);
        this.mColorBackgroundEnabled = ResourcesCompat.getColor(finder.getResources(),
                R.color.colorSensorItemEnabledBackground, null);
        // metadata
        this.mSensorBodyValueArray = ArrayAdapter.createFromResource(con,
                R.array.bodyParts, android.R.layout.simple_spinner_item);
        setEventHandlers();
        Log.i(TAG, "setComponents() via View");
    }

    public void setComponents(Activity finder) {
        Context con = finder;
        this.mSensorTitle = (TextView)finder.findViewById(R.id.sensorTitle);
        this.mSensorMacValue = (TextView)finder.findViewById(R.id.sensorMacValue);
        this.mSensorUuidValue = (TextView)finder.findViewById(R.id.sensorUuidValue);
        this.mEnableSensor = (CheckBox)finder.findViewById(R.id.enableSensor);
        this.mSensorBodyValue = (Spinner)finder.findViewById(R.id.sensorBodyValue);
        // visual formatting
        this.mSensorItemLayout = finder.findViewById(R.id.sensorItemLayout);
        this.mColorBackgroundDefault = ResourcesCompat.getColor(finder.getResources(),
                R.color.colorSensorItemBackground, null);
        this.mColorBackgroundEnabled = ResourcesCompat.getColor(finder.getResources(),
                R.color.colorSensorItemEnabledBackground, null);
        // metadata
        this.mSensorBodyValueArray = ArrayAdapter.createFromResource(con,
                R.array.bodyParts, android.R.layout.simple_spinner_item);
        setEventHandlers();
        Log.i(TAG, "setComponents() via Activity");
    }

    // ------------------------------------------------------------------------------------------
    public void setData(SensorItemData data) {
        this.mDataRef = data;
        this.mSensorTitle.setText( data.getTitle() );
        this.mSensorMacValue.setText( data.getMac() );
        this.mSensorUuidValue.setText( data.getUuid() );
        this.mEnableSensor.setChecked( data.isEnabled() );
        this.mSensorBodyValue.setEnabled( data.isEnabled() );
        if ( data.getBodyValue() != null ) {
            // https://stackoverflow.com/questions/2390102/how-to-set-selected-item-of-spinner-by-value-not-by-position
            int spinnerPos = mSensorBodyValueArray.getPosition( data.getBodyValue() );
            this.mSensorBodyValue.setSelection(spinnerPos);
        } else {
            Log.i(TAG,"body value (data) was null, resetting sensorBodyValue to head");
            this.mSensorBodyValue.setSelection(0);
        }
        Log.i(TAG, String.format( "setData() with Title = '%s', set Title = '%s'",
                data.getTitle(), this.mSensorTitle.getText() ));
    }

    // -----------------------------------------------------------------------------------------
    // also manages saving and rebuilding state when items are recycled
    private void setEventHandlers() {
        // checkbox
        this.mEnableSensor.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // checkbox controls the spinner
                mDataRef.setEnabled(isChecked);
                mDataRef.setBodyValue( mSensorBodyValue.getSelectedItem().toString() );

                mSensorBodyValue.setEnabled(isChecked);
                mSensorItemLayout.setBackgroundColor(isChecked ? mColorBackgroundEnabled : mColorBackgroundDefault);
                Log.i(TAG, String.format("enableSensor event: %b, bodyValue: %s",
                        mDataRef.isEnabled(), mDataRef.getBodyValue()));
            }
        });

        // spinner - track data change according to user selection
        // https://stackoverflow.com/questions/1337424/android-spinner-get-the-selected-item-change-event
        this.mSensorBodyValue.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {
                mDataRef.setBodyValue( mSensorBodyValue.getSelectedItem().toString() );
                Log.i(TAG, String.format("sensorBodyValue selected, value: %s", mDataRef.getBodyValue()));
            }
            @Override
            public void onNothingSelected(AdapterView<?> parentView) {
                mDataRef.setBodyValue( mSensorBodyValue.getSelectedItem().toString() );
                Log.i(TAG, String.format("sensorBodyValue selection lost, value: %s", mDataRef.getBodyValue()));
            }
        });

    }

}
