package random1.comp6733;

import android.content.Context;
import android.util.AttributeSet;
import android.util.Log;
import android.widget.LinearLayout;

import androidx.annotation.Nullable;

// this class is called every time the associated View is created from xml
// such as in the associated SensorItemAdapter class (which handles passing data to the view).
// this class is necessary for nice compound grouping properties in Layout Editor.
// yet, why is it so underutilised?

public class SensorItemView extends LinearLayout {
    private final String TAG = "SensorItemView";
    // NOTE: storage of this is unnecessary if we never do any data manipulation in this class
    //private SensorItemComponents components;

    // constructors
    public SensorItemView(Context context) {
        super(context);
        Log.i(TAG, "constructor (1 arg) finished");
    }

    public SensorItemView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        Log.i(TAG, "constructor (2 arg) finished");
    }

    public SensorItemView(Context context, @Nullable AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        Log.i(TAG, "constructor (3 arg) finished");
    }

    @Override
    protected void onFinishInflate() {
        // initialise your variables to their definitions in the xml file.
        // the xml file explicitly includes/refers to this class. hence, we do not need
        // to programmatically inflate() it here.
        super.onFinishInflate();
        //this.components = new SensorItemComponents();
        //this.components.setComponents(this);
        Log.i(TAG, "onFinishInflate() finished");
    }
}
