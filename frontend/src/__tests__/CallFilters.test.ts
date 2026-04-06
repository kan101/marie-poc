import { mount } from "@vue/test-utils";
import { describe, it, expect } from "vitest";
import CallFilters from "../components/CallFilters.vue";

describe("CallFilters", () => {
  it("renders search input", () => {
    const wrapper = mount(CallFilters, {
      props: {
        search: "",
        callerTypeFilter: "",
        urgentFilter: "",
      },
    });
    expect(wrapper.find("input").exists()).toBe(true);
  });

  it("renders caller type select", () => {
    const wrapper = mount(CallFilters, {
      props: {
        search: "",
        callerTypeFilter: "",
        urgentFilter: "",
      },
    });
    const selects = wrapper.findAll("select");
    expect(selects[0].exists()).toBe(true);
  });

  it("renders urgent filter select", () => {
    const wrapper = mount(CallFilters, {
      props: {
        search: "",
        callerTypeFilter: "",
        urgentFilter: "",
      },
    });
    const selects = wrapper.findAll("select");
    expect(selects[1].exists()).toBe(true);
  });

  it("emits update:search on input", async () => {
    const wrapper = mount(CallFilters, {
      props: {
        search: "",
        callerTypeFilter: "",
        urgentFilter: "",
      },
    });
    await wrapper.find("input").setValue("Johanna");
    expect(wrapper.emitted("update:search")).toBeTruthy();
    expect(wrapper.emitted("update:search")![0]).toEqual(["Johanna"]);
  });

  it("emits update:callerTypeFilter on change", async () => {
    const wrapper = mount(CallFilters, {
      props: {
        search: "",
        callerTypeFilter: "",
        urgentFilter: "",
      },
    });
    const selects = wrapper.findAll("select");
    await selects[0].setValue("new_client");
    expect(wrapper.emitted("update:callerTypeFilter")).toBeTruthy();
    expect(wrapper.emitted("update:callerTypeFilter")![0]).toEqual([
      "new_client",
    ]);
  });

  it("emits update:urgentFilter on change", async () => {
    const wrapper = mount(CallFilters, {
      props: {
        search: "",
        callerTypeFilter: "",
        urgentFilter: "",
      },
    });
    const selects = wrapper.findAll("select");
    await selects[1].setValue("true");
    expect(wrapper.emitted("update:urgentFilter")).toBeTruthy();
    expect(wrapper.emitted("update:urgentFilter")![0]).toEqual(["true"]);
  });

  it("displays current search value", () => {
    const wrapper = mount(CallFilters, {
      props: {
        search: "Johanna",
        callerTypeFilter: "",
        urgentFilter: "",
      },
    });
    expect((wrapper.find("input").element as HTMLInputElement).value).toBe(
      "Johanna"
    );
  });

  it("displays current caller type filter value", () => {
    const wrapper = mount(CallFilters, {
      props: {
        search: "",
        callerTypeFilter: "new_client",
        urgentFilter: "",
      },
    });
    const selects = wrapper.findAll("select");
    expect((selects[0].element as HTMLSelectElement).value).toBe("new_client");
  });
});
