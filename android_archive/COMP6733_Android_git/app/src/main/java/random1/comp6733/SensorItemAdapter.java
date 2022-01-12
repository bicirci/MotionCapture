package random1.comp6733;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class SensorItemAdapter extends RecyclerView.Adapter<SensorItemAdapter.ViewHolder>  {
    private final String TAG = "SensorItemAdapter";
    private List<SensorItemData> mDataList; // needs to be kept up to date with user input
    private LayoutInflater mInflater;

    // need to receive Context from Activity with the RecyclerView in it
    SensorItemAdapter(Context context, List<SensorItemData> data) {
        this.mInflater = LayoutInflater.from(context);
        this.mDataList = data;
        Log.i(TAG, "constructor finished");
    }

    // ------------------------------------------------------------------------------------------
    // https://stackoverflow.com/questions/51069491/the-difference-between-onviewrecycled-ondetachedfromrecyclerview-and-onviewde

    // 1. when RecyclerView needs an item for a row, inflate View from xml
    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        // https://developer.android.com/reference/android/support/v7/widget/RecyclerView.Adapter.html#onCreateViewHolder(android.view.ViewGroup,%20int)
        // https://developer.android.com/reference/android/view/LayoutInflater
        //View view = new SensorItemView(parent.getContext()); // this fails... why? wrong context?
        View view = mInflater.inflate(R.layout.sensor_item_view, parent, false);
        Log.i(TAG, String.format("new SensorItemView: %s", view.toString()));
        return new ViewHolder(view);
    }

    // 2. binds the data for that row. 'holder' is a ViewHolder that acts as an intermediate
    // data translator to the SensorItemView object.
    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        SensorItemData data = mDataList.get(position);
        Log.i(TAG, "new bind request (on ViewHolder)");
        holder.components.setData(data); // translation layer from data to view
    }

    // 3. clean-up row on recycle (lost visibility)... if needed
    //@Override
    //public void onViewRecycled (ViewHolder holder) { }

    // total number of rows
    @Override
    public int getItemCount() {
        return mDataList.size();
    }

    // -----------------------------------------------------------------------------------------
    // stores and recycles views as they are scrolled off screen
    public class ViewHolder extends RecyclerView.ViewHolder {
        private SensorItemComponents components;

        ViewHolder(View itemView) {
            super(itemView);
            this.components = new SensorItemComponents();
            this.components.setComponents(itemView);
            Log.i(TAG, "new ViewHolder constructor called");
        }
    }

}
