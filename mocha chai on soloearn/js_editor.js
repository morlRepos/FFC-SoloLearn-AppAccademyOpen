window.onload = (e)=>{
  const expect = chai.expect;
  mocha.setup('bdd');

  describe("Problems", function () {
    this.timeout(10000);
    describe("Has Loaded Correctly", function () {
        it('should be live', function () {
            expect(isLive).to.equal(true);
        })
     })
  });

}
