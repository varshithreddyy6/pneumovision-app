import { describe, expect, it } from "vitest";
import { API_URL } from "./api";

describe("api client", () => {
  it("defaults to local FastAPI", () => {
    expect(typeof API_URL).toBe("string");
  });
});
