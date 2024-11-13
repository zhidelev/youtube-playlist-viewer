import { test, expect } from '@playwright/test';


test.describe("navigation", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test.afterAll(async ({ page }) => {
    await page.close();
  });
  
  test('input visibility', async ({ page }) => {
    // expect that input is visible
    await expect(page.locator('input')).toBeVisible();
    const input = await page.locator('input');
    // expect that input is empty
    await expect(input).toHaveValue('');
    await expect(input).toHaveAttribute('id', 'playlist');
  });
  
  test('button visibility', async ({ page }) => {
  // expect that button is visible
  await expect(page.locator('button')).toBeVisible();
});

  test("input value", async ({ page }) => {
  const input = await page.locator('input');
  await input.fill('https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK');
  await expect(input).toHaveValue('https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK');
});
  test("header", async ({ page }) => {
    await page.goto('http://localhost:5174/');
    await expect(page).toHaveTitle('Conferences for me');
  });

});
