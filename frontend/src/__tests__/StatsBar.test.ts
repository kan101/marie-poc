import { mount, flushPromises } from "@vue/test-utils";
import { describe, it, expect, vi, beforeEach } from "vitest";
import StatsBar from "../components/StatsBar.vue";
import * as api from "../api";

const mockStats = {
  total_calls: 30,
  urgent: 11,
  email_sent: 19,
  no_action: 0,
  avg_duration_seconds: 29,
};

describe("StatsBar", () => {
  beforeEach(() => {
    vi.spyOn(api, "fetchStats").mockResolvedValue(mockStats);
  });

  it("renders stats after loading", async () => {
    const wrapper = mount(StatsBar);
    await flushPromises();
    expect(wrapper.text()).toContain("30");
    expect(wrapper.text()).toContain("11");
    expect(wrapper.text()).toContain("19");
  });

  it("shows loading state initially", () => {
    const wrapper = mount(StatsBar);
    expect(wrapper.text()).toContain("Loading");
  });

  it("formats avg duration correctly", async () => {
    const wrapper = mount(StatsBar);
    await flushPromises();
    expect(wrapper.text()).toContain("0:29");
  });
});
