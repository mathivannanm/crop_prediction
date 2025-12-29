package com.examplemathi.aiml.model;

public class Crop {
    private String crop;
    private String duration;
    private String season;
    private String soilType;
    private String avgWater;
    private String nNeed;
    private String pNeed;
    private String kNeed;
    private String urea;
    private String dap;
    private String mop;
    private String fertilizerTiming;
    private String extraTips;
    private String harvestingTips;

    public Crop() {}

    public Crop(String crop, String duration, String season, String soilType,
                String avgWater, String nNeed, String pNeed, String kNeed,
                String urea, String dap, String mop, String fertilizerTiming,
                String extraTips, String harvestingTips) {
        this.crop = crop;
        this.duration = duration;
        this.season = season;
        this.soilType = soilType;
        this.avgWater = avgWater;
        this.nNeed = nNeed;
        this.pNeed = pNeed;
        this.kNeed = kNeed;
        this.urea = urea;
        this.dap = dap;
        this.mop = mop;
        this.fertilizerTiming = fertilizerTiming;
        this.extraTips = extraTips;
        this.harvestingTips = harvestingTips;
    }

    // Getters and setters
    public String getCrop() { return crop; }
    public void setCrop(String crop) { this.crop = crop; }
    public String getDuration() { return duration; }
    public void setDuration(String duration) { this.duration = duration; }
    public String getSeason() { return season; }
    public void setSeason(String season) { this.season = season; }
    public String getSoilType() { return soilType; }
    public void setSoilType(String soilType) { this.soilType = soilType; }
    public String getAvgWater() { return avgWater; }
    public void setAvgWater(String avgWater) { this.avgWater = avgWater; }
    public String getnNeed() { return nNeed; }
    public void setnNeed(String nNeed) { this.nNeed = nNeed; }
    public String getpNeed() { return pNeed; }
    public void setpNeed(String pNeed) { this.pNeed = pNeed; }
    public String getkNeed() { return kNeed; }
    public void setkNeed(String kNeed) { this.kNeed = kNeed; }
    public String getUrea() { return urea; }
    public void setUrea(String urea) { this.urea = urea; }
    public String getDap() { return dap; }
    public void setDap(String dap) { this.dap = dap; }
    public String getMop() { return mop; }
    public void setMop(String mop) { this.mop = mop; }
    public String getFertilizerTiming() { return fertilizerTiming; }
    public void setFertilizerTiming(String fertilizerTiming) { this.fertilizerTiming = fertilizerTiming; }
    public String getExtraTips() { return extraTips; }
    public void setExtraTips(String extraTips) { this.extraTips = extraTips; }
    public String getHarvestingTips() { return harvestingTips; }
    public void setHarvestingTips(String harvestingTips) { this.harvestingTips = harvestingTips; }
}
