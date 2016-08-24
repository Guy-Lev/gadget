export default function(){
  this.transition(
    this.hasClass('slide'),
    this.toValue(true),
    this.use('toRight'),
    this.reverse('toLeft')
  );

  this.transition(
    this.hasClass('collapse-up'),
    this.toValue(true),
    this.use('toUp'),
    this.reverse('toDown')
  );

  this.transition(
    this.fromRoute('index'),
    this.toRoute('investigation-list'),
    this.use('toLeft'),
    this.reverse('toRight')
  );

  this.transition(
    this.fromRoute('investigation-list'),
    this.toRoute('investigation'),
    this.use('toLeft'),
    this.reverse('toRight')
  );

  this.transition(
    this.fromRoute('investigation-list'),
    this.toRoute('index'),
    this.use('toRight'),
    this.reverse('toLeft')
  );

  this.transition(
    this.fromRoute('investigation'),
    this.toRoute('index'),
    this.use('toRight'),
    this.reverse('toLeft')
  );

}
